import asyncio
import gd


async def main():
    # Initialize client
    client = gd.Client()

    # Search an user using name
    user: gd.Player = await client.search_user("notanerd1")

    print(user)


# Run the main function
asyncio.run(main())
