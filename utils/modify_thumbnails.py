import glob
import json
import os


def modify_thumbnails(directory):
    # Find all JSON files in the directory
    json_files = glob.glob(os.path.join(directory, '*.json'))
    
    for json_file in json_files:
        try:
            # Read the JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Function to recursively process JSON data
            def process_json(obj):
                if isinstance(obj, dict):
                    # If thumbnail field exists, replace .png with .svg
                    if 'thumbnail' in obj:
                        obj['thumbnail'] = obj['thumbnail'].replace('.png', '.svg')
                    # Process all values in the dictionary
                    for key in obj:
                        obj[key] = process_json(obj[key])
                elif isinstance(obj, list):
                    # Process all items in the list
                    return [process_json(item) for item in obj]
                return obj
            
            # Process the JSON data
            modified_data = process_json(data)
            
            # Write the modified data back to the file
            with open(json_file, 'w') as f:
                json.dump(modified_data, f, indent=1)
            
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON file: {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
