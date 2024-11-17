import asyncio
import gd

async def main():
    # Create a new client instance.
    client = gd.Client()

    # Log into the account
    await client.login(name="USERNAME", password="PASSWORD")

    # Comments on the level.
    await client.comment(message="sigma", level_id=111663149, percentage=0)

# Run the main function
asyncio.run(main())