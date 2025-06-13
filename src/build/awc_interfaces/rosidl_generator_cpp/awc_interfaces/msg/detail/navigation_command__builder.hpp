// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from awc_interfaces:msg/NavigationCommand.idl
// generated code does not contain a copyright notice

#ifndef AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__BUILDER_HPP_
#define AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "awc_interfaces/msg/detail/navigation_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace awc_interfaces
{

namespace msg
{

namespace builder
{

class Init_NavigationCommand_pose
{
public:
  explicit Init_NavigationCommand_pose(::awc_interfaces::msg::NavigationCommand & msg)
  : msg_(msg)
  {}
  ::awc_interfaces::msg::NavigationCommand pose(::awc_interfaces::msg::NavigationCommand::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::awc_interfaces::msg::NavigationCommand msg_;
};

class Init_NavigationCommand_navigate
{
public:
  Init_NavigationCommand_navigate()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigationCommand_pose navigate(::awc_interfaces::msg::NavigationCommand::_navigate_type arg)
  {
    msg_.navigate = std::move(arg);
    return Init_NavigationCommand_pose(msg_);
  }

private:
  ::awc_interfaces::msg::NavigationCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::awc_interfaces::msg::NavigationCommand>()
{
  return awc_interfaces::msg::builder::Init_NavigationCommand_navigate();
}

}  // namespace awc_interfaces

#endif  // AWC_INTERFACES__MSG__DETAIL__NAVIGATION_COMMAND__BUILDER_HPP_
