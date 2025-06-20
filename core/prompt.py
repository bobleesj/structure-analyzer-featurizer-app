import click
from click import echo, style

from core import folder


def get_user_input_folder_select(dir_names, file_type):
    click.echo(f"\nFolders with {file_type} files:")
    for i, dir_name in enumerate(dir_names, start=1):
        file_paths = folder.get_file_paths(dir_name)
        click.echo(f"{i}. {dir_name}, {len(file_paths)} files")
    click.echo("\nWould you like to process each folder above sequentially?")
    is_sequentially_processed = click.confirm("(Default: Y)", default=True)
    if is_sequentially_processed:
        dirs = {idx: name for idx, name in enumerate(dir_names, start=1)}
    else:
        dirs = get_folder_indices(dir_names)
    if len(dirs) == len(dir_names):
        click.echo("> Good! Let's process all the folders.")
    else:
        click.echo("> Good! You've chosen the following folders:")
        for i, dir_name in dirs.items():
            click.echo(f"{i}. {dir_name}")

    return dirs


def get_folder_indices(dirs_with_cif):
    while True:
        folder_numbers_str = click.prompt(
            "Enter the numbers corresponding to the folders listed above,"
            " separated by spaces. Ex) 1 2 3"
        )
        try:
            folder_indices = list(
                set(int(number) for number in folder_numbers_str.split())
            )
            # Check if all entered indices are valid
            if not all(1 <= i <= len(dirs_with_cif) for i in folder_indices):
                raise ValueError("Out of valid range.")
            # Map the indices to directory names
            selected_dirs = {i: dirs_with_cif[i - 1] for i in folder_indices}
            return selected_dirs
        except ValueError:
            click.echo("Please enter valid numbers, separated by spaces.")


def prompt_folder_progress(i, dir_name, dirs_total_count):
    """Display a progress header for folder processing with boundaries
    and folder information."""
    count = 70
    echo("\n")
    echo("=" * count)  # Top line of '=' characters
    echo(f"Processing {dir_name}, ({i} out of {dirs_total_count})")
    echo("=" * count)  # Bottom line of '=' characters


def prompt_progress_current(i, filename, supercell_atom_count, file_count):
    """Display the current progress for processing a file, highlighting
    the filename, atom count, and its order in the sequence."""
    echo(
        style(
            f"Processing {filename} with "
            f"{supercell_atom_count} atoms ({i}/{file_count})",
            fg="yellow",
        )
    )


def prompt_progress_finished(
    filename,
    supercell_atom_count,
    elapsed_time,
):
    """Display a completion message for a file, showing the filename,
    atom count, and the elapsed time in seconds."""
    echo(
        style(
            f"Processed {filename} with {supercell_atom_count} atoms in "
            f"{round(elapsed_time, 2)} s\n",
            fg="blue",
        )
    )


def prompt_file_saved(file_path):
    """Display a file has been saved."""
    echo(
        style(
            f"Saved {file_path}",
            fg="blue",
        )
    )
