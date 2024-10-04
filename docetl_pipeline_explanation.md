# DocETL Pipeline Configuration Explanation

This document provides a detailed explanation of the major components of a DocETL pipeline configuration, along with examples.

## 1. Datasets

Datasets are the input sources for your pipeline. They define where your data comes from and what format it's in.

- Name: A unique identifier for the dataset within your pipeline.
- Path: The location of your data file or database.
- Type: The format or storage type of your data (e.g., file, database).

Example:
```yaml
datasets:
  youtube_transcripts:
    path: ./data/youtube_transcripts.json
    type: file
```

## 2. Setting the Default Model

This specifies the language model to be used by default for operations that require AI processing.

Example:
```yaml
default_model: gpt-4o-mini
```

## 3. Creating Operations

Operations are the processing steps applied to your data. DocETL supports several types of operations:

### a) Map Operation

Applies a transformation to each item in the dataset independently.

Example:
```yaml
operations:
  - name: extract_key_concepts
    type: map
    output:
      schema:
        concepts: list[str]
    prompt: |
      Extract the key concepts from the following YouTube video transcript:
      {{ input.transcript }}
      List the key concepts, one per line.
```

### b) Reduce Operation

Combines multiple items in the dataset based on a key.

Example:
```yaml
operations:
  - name: summarize_concepts
    type: reduce
    reduce_key: 
      - video_id
    output:
      schema:
        summary: str
    prompt: |
      Summarize the key concepts for video {{ reduce_key }}:
      {% for item in values %}
      - {{ item.concepts | join(", ") }}
      {% endfor %}
```

### c) Resolve Operation

Identifies and resolves similar items in the dataset.

Example:
```yaml
operations:
  - name: resolve_similar_concepts
    type: resolve
    blocking_keys: 
      - concept
    blocking_threshold: 0.8
    comparison_prompt: |
      Are these two concepts similar?
      Concept 1: {{ input1.concept }}
      Concept 2: {{ input2.concept }}
    embedding_model: text-embedding-3-small
    output:
      schema:
        resolved_concept: str
    resolution_prompt: |
      Given these similar concepts:
      {% for item in inputs %}
      - {{ item.concept }}
      {% endfor %}
      Provide a single, standardized concept that best represents all of them.
```

### d) Unnest Operation

Flattens nested structures in your data.

Example:
```yaml
operations:
  - name: unnest_comments
    type: unnest
    unnest_key: comments
```

## 4. Defining Pipeline Steps

Pipeline steps define the sequence of operations to be applied to your data.

Example:
```yaml
pipeline:
  steps:
    - name: concept_extraction
      input: youtube_transcripts
      operations:
        - extract_key_concepts
    - name: concept_summarization
      input: concept_extraction
      operations:
        - summarize_concepts
        - resolve_similar_concepts
```

## 5. Configuring the Output

This specifies how and where the results of your pipeline should be saved.

Example:
```yaml
pipeline:
  output:
    type: file
    path: ./output/processed_concepts.json
    intermediate_dir: ./intermediate
```

## Complete Example

Here's a complete example of a DocETL pipeline YAML file that demonstrates how all these components work together:

```yaml
datasets:
  youtube_transcripts:
    path: ./data/youtube_transcripts.json
    type: file

default_model: gpt-4o-mini

operations:
  - name: extract_key_concepts
    type: map
    output:
      schema:
        concepts: list[str]
    prompt: |
      Extract the key concepts from the following YouTube video transcript:
      {{ input.transcript }}
      List the key concepts, one per line.

  - name: summarize_concepts
    type: reduce
    reduce_key: 
      - video_id
    output:
      schema:
        summary: str
    prompt: |
      Summarize the key concepts for video {{ reduce_key }}:
      {% for item in values %}
      - {{ item.concepts | join(", ") }}
      {% endfor %}

  - name: resolve_similar_concepts
    type: resolve
    blocking_keys: 
      - concept
    blocking_threshold: 0.8
    comparison_prompt: |
      Are these two concepts similar?
      Concept 1: {{ input1.concept }}
      Concept 2: {{ input2.concept }}
    embedding_model: text-embedding-3-small
    output:
      schema:
        resolved_concept: str
    resolution_prompt: |
      Given these similar concepts:
      {% for item in inputs %}
      - {{ item.concept }}
      {% endfor %}
      Provide a single, standardized concept that best represents all of them.

pipeline:
  steps:
    - name: concept_extraction
      input: youtube_transcripts
      operations:
        - extract_key_concepts
    - name: concept_summarization
      input: concept_extraction
      operations:
        - summarize_concepts
        - resolve_similar_concepts
  output:
    type: file
    path: ./output/processed_concepts.json
    intermediate_dir: ./intermediate
```

This pipeline would process YouTube transcripts, extract key concepts, summarize them for each video, resolve similar concepts across videos, and output the results to a JSON file.