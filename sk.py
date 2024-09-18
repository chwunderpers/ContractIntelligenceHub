import asyncio
import logging
import dotenv
import os

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior, FunctionChoiceType
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

from plugins import configure_services
from modules.negotiation.conversation import NegotiationConversation
from modules.stock.alphaVantagePlugin import AlphaVantagePlugin

async def main():
    #load environment variables
    dotenv.load_dotenv(override=True)

    # Initialize the kernel and other classes
    kernel = Kernel()
    configService = configure_services.configurationService(kernel)
    await configService.configure_services()
    negotiationService = NegotiationConversation()
    alphaVantageService = AlphaVantagePlugin(os.getenv("ALPHA_VANTAGE_KEY"))
    kernel.add_plugin(alphaVantageService, "alphaVantageService")
    kernel.add_plugin(negotiationService, "negotationService")
    

    # Add Azure OpenAI chat completion
    kernel.add_service(AzureChatCompletion(
        deployment_name="gpt-4o",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
    ))

    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("kernel").setLevel(logging.INFO)

    chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(
            max_tokens=1000,
            temperature=0.0,
            top_p=0.8,
            function_choice_behavior=FunctionChoiceBehavior(type=FunctionChoiceType.AUTO,
                maximum_auto_invoke_attempts=5,  
            )
    )      

    # Create a history of the conversation
    history = ChatHistory()
    with open("plugins/utils/system.jinja2", "r") as file:
            system_template = file.read()
    history.add_system_message(system_template)

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        # I need advice on the best negotiation strategy for the renewal of a contract with a single supplier for the agreementCode AG001!
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Start the conversation
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())