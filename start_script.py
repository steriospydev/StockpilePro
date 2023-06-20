import subprocess

subprocess.run(["python", "manage.py", "makemigrations"])
subprocess.run(["python", "manage.py", "mymigrations"])
subprocess.run(["python", "manage.py", "migrate"])
subprocess.run(["python", "manage.py", "loaddata", "start_data/data.json"])

#
# # Run tests
# # subprocess.run(["python", "manage.py", "test"])
