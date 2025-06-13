// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from awc_interfaces:msg/NavigationCommand.idl
// generated code does not contain a copyright notice

#ifndef AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__STRUCT_H_
#define AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in msg/NavigationCommand in the package awc_interfaces.
/**
  * A Pose with reference coordinate frame and timestamp
 */
typedef struct awc_interfaces__msg__NavigationCommand
{
  bool navigate;
  geometry_msgs__msg__PoseStamped pose;
} awc_interfaces__msg__NavigationCommand;

// Struct for a sequence of awc_interfaces__msg__NavigationCommand.
typedef struct awc_interfaces__msg__NavigationCommand__Sequence
{
  awc_interfaces__msg__NavigationCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} awc_interfaces__msg__NavigationCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__STRUCT_H_
