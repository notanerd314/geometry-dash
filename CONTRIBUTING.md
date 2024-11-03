# Contributing to `gdapi`

Thank you for your interest in contributing to gdapi! Please follow the rules below to make a meaningful contribution:

## Issues
To open an issue without being tagged as a "skill issue," you'll need:
- A clear description of what you're trying to do.
- The expected outcome and the actual outcome with the full traceback.
- Write the solutions that you tried.
- Verification that it's not entirely your fault (or else it’s a skill issue).

## Code Formatting
- Follow PEP8 for Python code.
- Run linters like `flake8` and `black` to check code quality.
- Add type hints where appropriate.
- Add documentation in **reStructuredText (reST) style**. This is an example:
  ```
  Sends an account comment to the account logged in.

  Cooldown is 15 seconds.

  :param message: The message to send.
  :type message: str
  :raises: ResponseError
  :return: The post ID of the sent post.
  ```

## Making Changes
- Write the commit message in **Present Simple tense**.
- The commit message should summarize all changes made, for example: "Add commenting and fix code formatting."
- Avoid changes that affect the entire code structure unless absolutely necessary.
- Add an extended description for large commits to list all changes made. Example:
  ``` 
  Add comments using the client's login session and fix code formatting in gd.py because notanerd used 2-character indents instead of 4. (I'm sick of this guy)
  ```

## Pull Requests
1. Push your branch:
   ```bash
   git push origin feature-or-bugfix-branch
   ```
2. Open a pull request:
   - Clearly explain the changes made.
   - State why the pull request is necessary.
3. Review Process:
   - Do not delete any files unless necessary.
   - Follow code formatting standards.
   - Include documentation for new functions.
   - Use your common sense!

## Bonus
If the issue or pull request is particularly helpful, you'll receive the **"chad"** tag!!! (wow)