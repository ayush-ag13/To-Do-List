from src import init_app
import os

app = init_app()

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0')

## local host 0.0.0.0 (all possible IP address )
