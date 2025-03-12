from .cli import main

# By convention, if someone runs python -m ckenc, Python uses __main__.py. Usually it just delegates to cli.py.

if __name__ == "__main__":
    main()
