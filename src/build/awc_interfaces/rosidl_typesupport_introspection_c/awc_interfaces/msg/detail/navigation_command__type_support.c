// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from awc_interfaces:msg/NavigationCommand.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "awc_interfaces/msg/detail/navigation_command__rosidl_typesupport_introspection_c.h"
#include "awc_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "awc_interfaces/msg/detail/navigation_command__functions.h"
#include "awc_interfaces/msg/detail/navigation_command__struct.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/pose_stamped.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  awc_interfaces__msg__NavigationCommand__init(message_memory);
}

void awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_fini_function(void * message_memory)
{
  awc_interfaces__msg__NavigationCommand__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_member_array[2] = {
  {
    "navigate",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(awc_interfaces__msg__NavigationCommand, navigate),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(awc_interfaces__msg__NavigationCommand, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_members = {
  "awc_interfaces__msg",  // message namespace
  "NavigationCommand",  // message name
  2,  // number of fields
  sizeof(awc_interfaces__msg__NavigationCommand),
  awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_member_array,  // message members
  awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_init_function,  // function to initialize message memory (memory has to be allocated)
  awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_type_support_handle = {
  0,
  &awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_awc_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, awc_interfaces, msg, NavigationCommand)() {
  awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  if (!awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_type_support_handle.typesupport_identifier) {
    awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &awc_interfaces__msg__NavigationCommand__rosidl_typesupport_introspection_c__NavigationCommand_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
