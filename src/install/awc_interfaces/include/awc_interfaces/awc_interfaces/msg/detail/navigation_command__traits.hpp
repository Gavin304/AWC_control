// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from awc_interfaces:msg/NavigationCommand.idl
// generated code does not contain a copyright notice

#ifndef AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__TRAITS_HPP_
#define AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "awc_interfaces/msg/detail/navigation_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace awc_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const NavigationCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: navigate
  {
    out << "navigate: ";
    rosidl_generator_traits::value_to_yaml(msg.navigate, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const NavigationCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: navigate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "navigate: ";
    rosidl_generator_traits::value_to_yaml(msg.navigate, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const NavigationCommand & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace awc_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use awc_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const awc_interfaces::msg::NavigationCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  awc_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use awc_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const awc_interfaces::msg::NavigationCommand & msg)
{
  return awc_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<awc_interfaces::msg::NavigationCommand>()
{
  return "awc_interfaces::msg::NavigationCommand";
}

template<>
inline const char * name<awc_interfaces::msg::NavigationCommand>()
{
  return "awc_interfaces/msg/NavigationCommand";
}

template<>
struct has_fixed_size<awc_interfaces::msg::NavigationCommand>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::PoseStamped>::value> {};

template<>
struct has_bounded_size<awc_interfaces::msg::NavigationCommand>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::PoseStamped>::value> {};

template<>
struct is_message<awc_interfaces::msg::NavigationCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__TRAITS_HPP_
