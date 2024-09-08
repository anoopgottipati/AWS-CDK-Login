import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_login.cdk_login_stack import CdkLoginStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_login/cdk_login_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkLoginStack(app, "cdk-login")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
