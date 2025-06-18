// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from awc_interfaces:msg/NavigationCommand.idl
// generated code does not contain a copyright notice
#include "awc_interfaces/msg/detail/navigation_command__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"

bool
awc_interfaces__msg__NavigationCommand__init(awc_interfaces__msg__NavigationCommand * msg)
{
  if (!msg) {
    return false;
  }
  // navigate
  // pose
  if (!geometry_msgs__msg__PoseStamped__init(&msg->pose)) {
    awc_interfaces__msg__NavigationCommand__fini(msg);
    return false;
  }
  return true;
}

void
awc_interfaces__msg__NavigationCommand__fini(awc_interfaces__msg__NavigationCommand * msg)
{
  if (!msg) {
    return;
  }
  // navigate
  // pose
  geometry_msgs__msg__PoseStamped__fini(&msg->pose);
}

bool
awc_interfaces__msg__NavigationCommand__are_equal(const awc_interfaces__msg__NavigationCommand * lhs, const awc_interfaces__msg__NavigationCommand * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // navigate
  if (lhs->navigate != rhs->navigate) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__PoseStamped__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  return true;
}

bool
awc_interfaces__msg__NavigationCommand__copy(
  const awc_interfaces__msg__NavigationCommand * input,
  awc_interfaces__msg__NavigationCommand * output)
{
  if (!input || !output) {
    return false;
  }
  // navigate
  output->navigate = input->navigate;
  // pose
  if (!geometry_msgs__msg__PoseStamped__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  return true;
}

awc_interfaces__msg__NavigationCommand *
awc_interfaces__msg__NavigationCommand__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  awc_interfaces__msg__NavigationCommand * msg = (awc_interfaces__msg__NavigationCommand *)allocator.allocate(sizeof(awc_interfaces__msg__NavigationCommand), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(awc_interfaces__msg__NavigationCommand));
  bool success = awc_interfaces__msg__NavigationCommand__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
awc_interfaces__msg__NavigationCommand__destroy(awc_interfaces__msg__NavigationCommand * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    awc_interfaces__msg__NavigationCommand__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
awc_interfaces__msg__NavigationCommand__Sequence__init(awc_interfaces__msg__NavigationCommand__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  awc_interfaces__msg__NavigationCommand * data = NULL;

  if (size) {
    data = (awc_interfaces__msg__NavigationCommand *)allocator.zero_allocate(size, sizeof(awc_interfaces__msg__NavigationCommand), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = awc_interfaces__msg__NavigationCommand__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        awc_interfaces__msg__NavigationCommand__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
awc_interfaces__msg__NavigationCommand__Sequence__fini(awc_interfaces__msg__NavigationCommand__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      awc_interfaces__msg__NavigationCommand__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

awc_interfaces__msg__NavigationCommand__Sequence *
awc_interfaces__msg__NavigationCommand__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  awc_interfaces__msg__NavigationCommand__Sequence * array = (awc_interfaces__msg__NavigationCommand__Sequence *)allocator.allocate(sizeof(awc_interfaces__msg__NavigationCommand__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = awc_interfaces__msg__NavigationCommand__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
awc_interfaces__msg__NavigationCommand__Sequence__destroy(awc_interfaces__msg__NavigationCommand__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    awc_interfaces__msg__NavigationCommand__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
awc_interfaces__msg__NavigationCommand__Sequence__are_equal(const awc_interfaces__msg__NavigationCommand__Sequence * lhs, const awc_interfaces__msg__NavigationCommand__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!awc_interfaces__msg__NavigationCommand__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
awc_interfaces__msg__NavigationCommand__Sequence__copy(
  const awc_interfaces__msg__NavigationCommand__Sequence * input,
  awc_interfaces__msg__NavigationCommand__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(awc_interfaces__msg__NavigationCommand);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    awc_interfaces__msg__NavigationCommand * data =
      (awc_interfaces__msg__NavigationCommand *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!awc_interfaces__msg__NavigationCommand__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          awc_interfaces__msg__NavigationCommand__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!awc_interfaces__msg__NavigationCommand__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
