from sk import create_negotiation_strategy
import asyncio

async def main():
    print(await create_negotiation_strategy("I need advice on the best negotiation strategy for the renewal of a contract with a single supplier for the agreementCode AG001!"))

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())