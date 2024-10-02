# DocETL Technology Stack

This document outlines the key technology choices and architecture decisions for the DocETL project.

## Core Technologies

1. **Python**: Version 3.10+
   - Chosen for its rich ecosystem of data processing and machine learning libraries
   - Offers good performance and ease of use for complex tasks

2. **Poetry**: Dependency management and packaging
   - Provides reproducible builds and easy dependency management
   - Simplifies the development and deployment process

3. **YAML**: Configuration language for pipeline definitions
   - Offers a human-readable and easy-to-write format for defining complex pipelines
   - Allows for declarative pipeline specifications

## Key Dependencies

1. **litellm**: ^1.42.1
   - Provides a unified interface for working with various LLM providers
   - Simplifies integration and switching between different LLM models

2. **pydantic**: ^2.9.2
   - Used for data validation and settings management
   - Ensures type safety and helps catch errors early in development

3. **scikit-learn**: ^1.5.2
   - Utilized for various machine learning tasks, particularly in optimization processes
   - Provides robust implementations of common ML algorithms

4. **typer**: ^0.12.5
   - Used for building the command-line interface
   - Offers an intuitive way to create CLI applications with Python type hints

5. **tqdm** and **rich**: 
   - Enhance the user experience with progress bars and rich console output
   - Improve the readability of console output during pipeline execution

## Optional Dependencies

- **python-docx**, **openpyxl**, **python-pptx**: For parsing various document formats
- **azure-ai-documentintelligence**: For advanced document processing capabilities

## Architecture Decisions

1. **Modular Design**: 
   - The project is structured into separate modules (e.g., operations, optimizers) for better maintainability and extensibility

2. **Pipeline Abstraction**: 
   - Use of a pipeline concept to represent complex document processing tasks
   - Allows for easy composition and reuse of processing steps

3. **Optimizer Component**: 
   - Dedicated module for optimizing pipeline performance and accuracy
   - Leverages LLM agents to experiment with different pipeline configurations

4. **Extensible Operator System**: 
   - Designed to allow easy addition of new operators for different processing tasks
   - Promotes flexibility and adaptability to various use cases

5. **Declarative Configuration**: 
   - Use of YAML for pipeline definitions enables a low-code approach
   - Separates the pipeline logic from its implementation, improving maintainability

This tech stack is subject to change as the project evolves and new requirements emerge. Regular reviews will be conducted to ensure the chosen technologies continue to meet the project's needs effectively.