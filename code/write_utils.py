import os
import csv
import json
import logging

def save_precinct_result_to_csv(result, output_path):
    """Save precinct result to CSV file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not result or "results" not in result:
        return
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['position_name', 'candidate_name', 'votes', 'percentage'])
        
        # Write data
        for position in result["results"]:
            position_name = position.get("position_name", "")
            for candidate in position.get("candidates", []):
                writer.writerow([
                    position_name,
                    candidate.get("name", ""),
                    candidate.get("votes", 0),
                    candidate.get("percentage", 0)
                ])

def get_completed_precincts(base_dir):
    """Get set of already processed precinct codes"""
    completed = set()
    if not os.path.exists(base_dir):
        return completed
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                precinct_code = os.path.splitext(file)[0]
                completed.add(precinct_code)
    
    return completed

def organize_existing_csvs(base_dir):
    """Organize existing CSV files"""
    if not os.path.exists(base_dir):
        return
    
    logging.info(f"Organizing existing CSVs in {base_dir}")

def write_checkpoint(metadata, precinct_code, path="checkpoint.json"):
    """Write checkpoint data to JSON file"""
    checkpoint_data = {
        "region": {"code": metadata["region_code"], "name": metadata["region"]},
        "province": {"code": metadata["province_code"], "name": metadata["province"]},
        "city": {"code": metadata["city_code"], "name": metadata["city"]},
        "barangay": {"code": metadata["barangay_code"], "name": metadata["barangay"]},
        "precinct": {"code": precinct_code}
    }
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2)