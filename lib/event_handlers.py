from redis_om import Migrator, MigrationError
from redis.exceptions import ConnectionError
import config

async def startup_handler():
    try:
        Migrator().run()
        print(config.node_env)
        print("Server start!")
    except MigrationError as merror:
        print(str(merror))
    except ConnectionError as cerror:
        print("Fail connecting to database")
        print(str(cerror))

async def shutdown_handler():
    print("Server closed, bye bye")
    
    