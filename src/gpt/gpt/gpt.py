#!/usr/bin/env python3
from .audio import record_audio, speech_to_text, text_to_speech, play_audio
import os 
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import threading
import sounddevice as sd
import re
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

# Get the absolute path to the audio_files directory
from ament_index_python.packages import get_package_share_directory
package_share_directory = get_package_share_directory('gpt')
audio_files_path = os.path.join(package_share_directory, 'audio_files')

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class GPTNode(Node):
    def __init__(self):
        super().__init__('gpt_node')
        self.publisher_ = self.create_publisher(String, '/chatgpt_command', 10)

    def publish_navigation_command(self, command_json):
        msg = String()
        msg.data = command_json
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published navigation command: {command_json}')

with open(os.path.join(os.path.dirname(__file__), "prompt.txt"), "r") as file:
    system_prompt = file.read()
    messages = [{"role": "system", "content": system_prompt}]

def main():
    run_gpt()

def run_gpt():
    rclpy.init()
    gpt_node = GPTNode()
    control_number = 0

    try:
        while True:     
            # content = input("User: ") keyboard input

            chime_1 = threading.Thread(target=lambda: os.system(f'aplay {os.path.join(audio_files_path, "init.wav")}'))
            chime_1.start()

            content = speech_to_text(record_audio()) # speech input

            chime_2 = threading.Thread(target=lambda: os.system(f'aplay {os.path.join(audio_files_path, "conf.wav")}'))
            chime_2.start()

            messages.append ({"role": "user", "content": content})
            completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=200, 
                temperature=0.2,
            )
            chat_response = completion.choices[0].message.content
            match = re.search(r'\{(\d+)\}', chat_response)
            if match:
                control_number = int(match.group(1))
                print(control_number) # send this number to control system
                chat_response = re.sub(r'\{\d+\}', '', chat_response)
            else:
                control_number = 0
            print(f'alex: {chat_response}')
            messages.append ({"role": "assistant", "content": chat_response})

            text_to_speech(chat_response)
            play_audio()

            # Extract JSON part of the response if it contains "navigate"
            if "navigate" in chat_response:
                try:
                    json_start = chat_response.index('{')
                    json_end = chat_response.rindex('}') + 1
                    command_json = chat_response[json_start:json_end]
                    gpt_node.publish_navigation_command(command_json)
                except (ValueError, json.JSONDecodeError) as e:
                    print(f"Error extracting or parsing JSON: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()
        return control_number
    
if __name__ == "__main__":
    main()