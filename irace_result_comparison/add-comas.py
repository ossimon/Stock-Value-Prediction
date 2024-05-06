def add_comas(input_file_name, output_file_name):
    with open(input_file_name, 'r') as infile, open(output_file_name, 'w') as outfile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                outfile.write(line)
            else:
                outfile.write(','.join(line.split()) + '\n')

add_comas('default_params.csv', 'default_params_modified.csv')
add_comas('irace_optimized.csv', 'irace_optimized_modified.csv')