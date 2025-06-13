// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from awc_interfaces:msg/NavigationCommand.idl
// generated code does not contain a copyright notice

#ifndef AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__STRUCT_HPP_
#define AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__awc_interfaces__msg__NavigationCommand __attribute__((deprecated))
#else
# define DEPRECATED__awc_interfaces__msg__NavigationCommand __declspec(deprecated)
#endif

namespace awc_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct NavigationCommand_
{
  using Type = NavigationCommand_<ContainerAllocator>;

  explicit NavigationCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->navigate = false;
    }
  }

  explicit NavigationCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->navigate = false;
    }
  }

  // field types and members
  using _navigate_type =
    bool;
  _navigate_type navigate;
  using _pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _pose_type pose;

  // setters for named parameter idiom
  Type & set__navigate(
    const bool & _arg)
  {
    this->navigate = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    awc_interfaces::msg::NavigationCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const awc_interfaces::msg::NavigationCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      awc_interfaces::msg::NavigationCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      awc_interfaces::msg::NavigationCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__awc_interfaces__msg__NavigationCommand
    std::shared_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__awc_interfaces__msg__NavigationCommand
    std::shared_ptr<awc_interfaces::msg::NavigationCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const NavigationCommand_ & other) const
  {
    if (this->navigate != other.navigate) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    return true;
  }
  bool operator!=(const NavigationCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct NavigationCommand_

// alias to use template instance with default allocator
using NavigationCommand =
  awc_interfaces::msg::NavigationCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace awc_interfaces

#endif  // AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__STRUCT_HPP_
