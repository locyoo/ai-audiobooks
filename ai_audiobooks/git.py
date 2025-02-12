from dataclasses import dataclass
from pathlib import Path
from git import Repo
import shutil


@dataclass
class GitWorkingDirectory:
    repo: Repo
    input_file_copy: Path
    working_dir: Path

    @property
    def text_file_path(self) -> Path:
        return self.working_dir / f"{self.input_file_copy.stem}.txt"

    def delete(self) -> None:
        """Delete the working directory."""
        shutil.rmtree(self.working_dir)

    @staticmethod
    def from_file(file: Path) -> "GitWorkingDirectory":
        """Create a GitWorkingDirectory from a file."""
        working_dir = file.parent
        repo = Repo(working_dir)
        return GitWorkingDirectory(
            repo=repo, input_file_copy=file, working_dir=working_dir
        )


def git_create_working_dir(
    *, input_file: Path, working_directory_root: Path = Path("output")
) -> GitWorkingDirectory:
    """Create a working directory for the input file."""
    # Create the working directory.
    working_dir = working_directory_root / input_file.stem
    working_dir.mkdir(exist_ok=True, parents=True)

    # Initialize a git repository.
    repo = Repo.init(working_dir)

    # Copy the input file to the working directory.
    input_file_copy = working_dir / input_file.name
    shutil.copy(input_file, input_file_copy)

    # Add the input file to the git repository.
    repo.index.add([input_file_copy.relative_to(working_dir)])

    # Make the initial commit.
    repo.index.commit("Initial commit")

    # Return the working directory.
    return GitWorkingDirectory(
        repo=repo, input_file_copy=input_file_copy, working_dir=working_dir
    )
