from pprint import pprint
import inquirer
from inquirer.themes import WordleTheme

questions = [
    inquirer.List(
        "size",
        message="What size do you need?",
        choices=["Jumbo", "Large", "Standard", "Medium", "Small", "Micro"],
    ),
]

answers = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore
pprint(answers)
