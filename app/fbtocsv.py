import os

def remove_quotes_and_spaces(filename):
    with open(filename, 'r') as file:
        content = file.read()
        modified_content = content.replace('"', '').replace(' ', '')
        file.close()
    with open(filename, 'w') as file:
        file.write(modified_content)
        file.close()
    with open(filename, 'r') as file:
        lines = file.readlines()
        if lines:
            lines.pop(0)
        file.close()
    with open(filename, 'w') as file:
        file.writelines(lines)
        file.close()

def file_to_list(filename):
    with open(filename, 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
        file.close()
        return lines

def fbexport(statement, filename):
    os.system('fbexport -Sc -H localhost \
    -D /app/ce.fdb \
    -F "'+filename+'" -Q "'+statement+'"')

def count(relation_name):
    return os.popen("echo set heading off \; select count\(*\) from "+relation_name+"\; | isql /app/ce.fdb").read().replace('\n', '').replace(' ', '')

# Get the password and set it as environment variable
sysdba_pas = os.popen("cat /opt/firebird/SYSDBA.password | grep ISC_PASSWD | awk -F '=' '{ print $2 }'").read().replace('\n', '')
os.environ['ISC_USER'] = "SYSDBA"
os.environ['ISC_PASSWORD'] = sysdba_pas

# Start the server
os.system("/etc/init.d/firebird start")

# Create the helper relations (table names) file
os.chdir("/app")
os.mkdir("output")
os.chdir("./output")
filename = '_relations.csv'
fbexport("select rdb\$relation_name from rdb\$relations where coalesce(rdb\$relation_type, 0) = 0", filename)
remove_quotes_and_spaces(filename)
with open(filename, 'r') as file:
    lines = file.readlines()
    filtered_lines = [line for line in lines if not '$' in line] # remove system tables from this list
with open(filename, 'w') as file:
    file.writelines(filtered_lines)

# get all the table names
relations = file_to_list(filename)

# export every relation data to csv
for relation in relations:
    # no use exporting empty tables
    if (count(relation) == '0'):
        print('Empty Table!')
    else:
        filename = '/tmp/' + relation + '_columns.txt'
        # this statement gets all the column names from a relation (table) that are not a BLOB type (261)
        select_statement = "select rf.rdb\$field_name from rdb\$relation_fields rf join rdb\$fields f on f.rdb\$field_name = rf.rdb\$field_source where rf.rdb\$relation_name = \'"+relation+"\' and f.rdb\$field_type <> 261"
        fbexport(select_statement, filename)
        remove_quotes_and_spaces(filename)
        relation_columns = file_to_list(filename)
        os.remove(filename)
        select_statement = 'SELECT ' + ', '.join(relation_columns) + ' FROM ' + relation
        fbexport(select_statement, relation + '.csv')