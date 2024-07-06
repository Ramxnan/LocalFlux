from Part_2.driver import driver_part2

import os
if __name__ == "__main__":
    input_dir_path="C:\\Users\\raman\\OneDrive - Amrita vishwa vidyapeetham\\ASE\\Projects\\NBA\\NBA_v3\\dev_19.1\\flux\\nba\\Part_2\\TestFiles"
    output_dir_path="C:\\Users\\raman\\OneDrive - Amrita vishwa vidyapeetham\\ASE\\Projects\\NBA\\NBA_v3\\dev_19.1\\flux\\nba\\Part_2\\TestFiles"
    errors=driver_part2(input_dir_path, output_dir_path)
    print(errors)

    #os.startfile(os.path.join(output_dir_path, errors))