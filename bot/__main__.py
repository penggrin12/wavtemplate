"""
This whole file just feels weird. I should do something about it.
"""

async def _close_dbs():
    from . import db

    print("Closing the db connections...")

    await db.users_db.close()


def _main():
    from .loops import loop

    try:
        from .main import main

        main(loop)
    finally:
        loop.run_until_complete(_close_dbs())

    print("bye")


_main()
