# Contributing to Naukri Job Scraper

First off, thank you for considering contributing to this project! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions you've considered**

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

#### Pull Request Guidelines

- Follow the existing code style
- Update documentation as needed
- Add tests if applicable
- Ensure your code doesn't break existing functionality
- Keep pull requests focused on a single feature/fix

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Use docstrings for functions and classes

## Development Setup

1. Clone your fork
2. Install dependencies: `pip install -r requirements.txt`
3. Install dev dependencies: `pip install -r requirements-dev.txt` (if available)
4. Create a `.env` file from `.env.example`
5. Set up the MySQL database using `schema/database_schema.sql`

## Testing

Before submitting a pull request:

1. Test your changes thoroughly
2. Ensure the scraper runs without errors
3. Verify email functionality works
4. Check database operations complete successfully

## Questions?

Feel free to open an issue with the `question` label if you have any questions!

Thank you for contributing! 🙏