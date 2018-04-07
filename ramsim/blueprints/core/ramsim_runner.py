from ... import db
from ...models import CodeExec
from ...ramsim import Runner, Parser, ParserException, RunnerException
from flask import url_for
from uuid import uuid4 as gen_uuid
import os
import re

# @TODO remove
import pprint

class RamsimRunner(object):
    
    @staticmethod
    def add_to_db_and_exec(code, svars):
        uuid = str(gen_uuid())
        path = CodeExec.add_to_db(uuid, svars)

        try:
            with open(path, "w") as f:
                f.write(code)

        except IOError:
            return "Something went wrong"

        RamsimRunner.handle_request(uuid)

        return uuid
    
    @staticmethod
    def vars_to_list(vars):
        if vars:
            return [int(x) for x in vars.split(";")]
        else:
            return []


    @staticmethod
    def list_to_vars(vars):
        return ";".join(map(str, vars))


    @staticmethod
    def get_code_svars_from_uuid(uuid):

        try:
            code_exec = CodeExec.query.filter_by(uuid=uuid).first()
            if not code_exec:
                return None

            svars = RamsimRunner.vars_to_list(code_exec.svars)
            code = ""

            with open(code_exec.codepath, "r") as f:
                code = f.read()
            
            # If there was no error, load the execution csv file
            csvlist = []
            if not code_exec.error:
                with open(code_exec.csvpath, "r") as f:
                    for line in f.readlines():
                        csvlist.append(line[1:-2].split('";"'))

            return {
                "svars": svars,
                "code" : code,
                "error": code_exec.error,
                "errors": code_exec.errors,
                "result": RamsimRunner.vars_to_list(code_exec.result),
                "exectable": csvlist[1:],
                "csvpath": code_exec.csvpath
            }

        except IOError:
            return None


    @staticmethod
    def handle_request(uuid):

        code_exec = CodeExec.query.filter_by(uuid=uuid).first()
        if not code_exec:
            return
        
        try:
            p = Parser(code_exec.codepath)
            r = Runner(p.get_parsed_dict(), debug=False)
            r.fill_input(RamsimRunner.vars_to_list(code_exec.svars))
            res = r.execute_program()

            # Add Results to DB
            code_exec.error = False
            code_exec.errors = ""
            code_exec.result = RamsimRunner.list_to_vars(res)

            # Store execution table
            code_exec.csvpath = f"{code_exec.codepath}.csv"
            r.export_exec_table(code_exec.csvpath)

            print(f"DEBUG")
            pprint.pprint(r.get_exec_table())

        except (ParserException, RunnerException) as e:
            code_exec.error = True
            code_exec.errors = str(e)
            code_exec.result = ""

        except ValueError:
            code_exec.error = True
            code_exec.errors = "Something went wrong. Check your svars"
            code_exec.result = ""
        
        except IOError:
            code_exec.error = True
            code_exec.errors = "Internal error."
            code_exec.result = ""

        finally:
            db.session.commit()
