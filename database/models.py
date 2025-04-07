import importlib

def perform_db_action(table, action, **kwargs):
    try:
        class_name = "".join(word.capitalize() for word in table.split("_"))+"Service"
        module = importlib.import_module(f"database.{table}")
        table_class = getattr(module, class_name)
        instance = table_class()
        if hasattr(instance, action):
            return getattr(instance, action)(**kwargs)
        else:
            raise AttributeError(f"{class_name} has no method '{action}'")
    
    except ModuleNotFoundError:
        print(f"Error: Module 'database.{table}' not found.")
        return None
    except AttributeError as e:
        print(f"Error: {e}")
        return None