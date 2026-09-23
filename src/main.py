import dotenv 
import login_gate

# Loading the .env file.
dotenv.load_dotenv(
    dotenv_path="../.env",
    override=False
)


if __name__ == "__main__":
    login_gate.launch()