"""
Program launch.

The program uses from the console. To run it, you need to go to the project directory,
use the command in the console:

$ python main.py --host HOST --port PORT --user USER --password PASSWORD
--db_name DB_NAME --schema_name SCHEMA_NAME --engine ENGINE --direction DIRECTION

"""
import argparse
from diagram_builder import PlantUMLBilder
from postgre_handler import ERAlchemyHandler
from postgre_handler import PostgreSQL_handler
from dbml_renderer_handler import DBMLRenderer


def main(host, port, user, password, db_name, schema_name, engine=None, direction='1'):
    try:
        answer = \
            PostgreSQL_handler(host, port, user, password, db_name, schema_name).start_handler()
    except NameError:
        print('Attention! In db not tables.')
    else:
        if answer:
            tables_structure, foreign_keys_for_diagram_builder, keys_in_table, \
                number_of_keys, primary_keys, column_types = answer
            if engine == 'plantuml':
                PlantUMLBilder(db_name).start_handler(
                    tables_structure, foreign_keys_for_diagram_builder, keys_in_table, primary_keys, direction
                )
            elif engine == 'dbml-r':
                DBMLRenderer(db_name).start_handler(
                    tables_structure, foreign_keys_for_diagram_builder, primary_keys, column_types, direction
                )
            elif engine == 'eralchemy':
                ERAlchemyHandler(db_name, user, password, host).start_handler()
            # Will doing diagrams by 3 way if type of engine does not choose.
            else:
                DBMLRenderer(db_name).start_handler(
                     tables_structure, foreign_keys_for_diagram_builder, primary_keys, column_types, direction
                )
                PlantUMLBilder(db_name).start_handler(
                    tables_structure, foreign_keys_for_diagram_builder, keys_in_table, primary_keys, direction
                )
                ERAlchemyHandler(db_name, user, password, host).start_handler()

# Launching the program from console.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diagram Builder")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--port", required=True, help="Database port")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--db_name", required=True, help="Database name")
    parser.add_argument("--schema_name", required=True, help="Schema name")
    parser.add_argument(
        "--engine",
        help="Select how the diagram is rendered. Available 2 type.\n"
             "PlantUML - write 'plantuml'.\nDBML-renderer - write 'dbml-r'.\n"
             "Eralchemy - write 'eralchemy'."
    )
    parser.add_argument(
        "--direction", required=False, help="By default is '1', can be '2'. Affects the layout of tables."
    )

    args = parser.parse_args()
    main(args.host, args.port, args.user, args.password, args.db_name, args.schema_name, args.engine, args.direction)
