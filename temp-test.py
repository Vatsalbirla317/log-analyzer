from utils.parser import parse_log_file
df = parse_log_file("logs/sample2.json")
print(df.head())
