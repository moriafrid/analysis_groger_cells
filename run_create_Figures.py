import os
before_after='_after_shrink'
base="python "
base="sbatch execute_python_script.sh "
#os.system("python reorgenize_results.py")
os.system(base+" create_Figure1.py ")
os.system(base+" create_Figure2.py ")
os.system(base+" create_Figure3.py ")
