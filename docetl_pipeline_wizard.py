import yaml
import os

def get_input(prompt, default=None, multiline=False):
    try:
        if multiline:
            print(f"{prompt} (Type your input, then enter 'END' on a new line when finished):")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            return '\n'.join(lines)
        else:
            if default:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                return user_input if user_input else default
            return input(f"{prompt}: ").strip()
    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting...")
        exit(1)

def get_list_input(prompt):
    print(f"{prompt} (Enter one item per line, press Enter twice to finish):")
    items = []
    try:
        while True:
            item = input().strip()
            if not item:
                if items:  # Only break if we have at least one item
                    break
                print("Please enter at least one item.")
            else:
                items.append(item)
    except KeyboardInterrupt:
        print("\nInput interrupted. Using items entered so far.")
    return items

def create_pipeline_yaml():
    pipeline = {}

    try:
        # Step 1: Datasets
        print("\n--- Step 1: Define Datasets ---")
        pipeline['datasets'] = {}
        while True:
            dataset_name = get_input("Enter dataset name (or press Enter to finish)")
            if not dataset_name:
                if not pipeline['datasets']:
                    print("Please define at least one dataset.")
                    continue
                break
            dataset_path = get_input("Enter dataset path")
            dataset_type = get_input("Enter dataset type (e.g., file, database)")
            pipeline['datasets'][dataset_name] = {
                'path': dataset_path,
                'type': dataset_type
            }

        # Step 2: Default Model
        print("\n--- Step 2: Set Default Model ---")
        pipeline['default_model'] = get_input("Enter default model (e.g., gpt-4o-mini)")

        # Step 3: Operations
        print("\n--- Step 3: Define Operations ---")
        pipeline['operations'] = []
        while True:
            print("\nDefining a new operation:")
            operation = {}
            operation['name'] = get_input("Enter operation name")
            operation['type'] = get_input("Enter operation type (e.g., map, reduce, resolve, unnest)")
            
            if operation['type'] == 'map':
                operation['output'] = {'schema': {}}
                output_schema = get_list_input("Enter output schema keys (one per line)")
                for key in output_schema:
                    operation['output']['schema'][key] = get_input(f"Enter type for {key}")
                operation['prompt'] = get_input("Enter prompt for the operation", multiline=True)
            
            elif operation['type'] == 'reduce':
                operation['reduce_key'] = get_list_input("Enter reduce keys (one per line)")
                operation['output'] = {'schema': {}}
                output_schema = get_list_input("Enter output schema keys (one per line)")
                for key in output_schema:
                    operation['output']['schema'][key] = get_input(f"Enter type for {key}")
                operation['prompt'] = get_input("Enter prompt for the operation", multiline=True)
            
            elif operation['type'] == 'resolve':
                operation['blocking_keys'] = get_list_input("Enter blocking keys (one per line)")
                operation['blocking_threshold'] = float(get_input("Enter blocking threshold (e.g., 0.6162)"))
                operation['comparison_prompt'] = get_input("Enter comparison prompt", multiline=True)
                operation['embedding_model'] = get_input("Enter embedding model")
                operation['output'] = {'schema': {}}
                output_schema = get_list_input("Enter output schema keys (one per line)")
                for key in output_schema:
                    operation['output']['schema'][key] = get_input(f"Enter type for {key}")
                operation['resolution_prompt'] = get_input("Enter resolution prompt", multiline=True)
            
            elif operation['type'] == 'unnest':
                operation['unnest_key'] = get_input("Enter unnest key")

            pipeline['operations'].append(operation)
            
            if get_input("Add another operation? (y/n)").lower() != 'y':
                break

        # Step 4: Pipeline Steps
        print("\n--- Step 4: Define Pipeline Steps ---")
        pipeline['pipeline'] = {'steps': []}
        while True:
            step = {}
            step['name'] = get_input("Enter step name")
            step['input'] = get_input("Enter input dataset name")
            step['operations'] = get_list_input("Enter operation names for this step (one per line)")
            pipeline['pipeline']['steps'].append(step)
            
            if get_input("Add another step? (y/n)").lower() != 'y':
                break

        # Step 5: Output Configuration
        print("\n--- Step 5: Configure Output ---")
        pipeline['pipeline']['output'] = {
            'type': get_input("Enter output type (e.g., file)"),
            'path': get_input("Enter output path"),
            'intermediate_dir': get_input("Enter intermediate results directory")
        }

        # Write to YAML file
        filename = get_input("Enter filename for the YAML file", "pipeline.yaml")
        with open(filename, 'w') as file:
            yaml.dump(pipeline, file, default_flow_style=False)

        print(f"\nPipeline YAML file '{filename}' has been created successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("The wizard will now exit. Please run it again to create your pipeline.")

if __name__ == "__main__":
    create_pipeline_yaml()