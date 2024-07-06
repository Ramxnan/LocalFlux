from Part_1.driver import driver_part1

import os

if __name__ == "__main__":

    
    # data={
    #     "Teacher":"Dr. S. S. Patil",                                                              #set teacher name
    #     "Academic_year":"2022-2023",  
    #     "Batch":2019,
    #     "Branch":"MEE",                                                                          #set branch
    #     "Subject_Name":"PCE",
    #     "Subject_Code":"19MEE444",
    #     "Section":"A",
    #     "Semester":"Even",
    #     "Number_of_Students":47,
    #     "Number_of_COs":4}
    
    data={
        "Teacher":"Dr. S. S. Patil",                                                              #set teacher name
        "Academic_year":"2022-2023",  
        "Batch":2019,
        "Branch":"CSE",                                                                          #set branch
        "Subject_Name":"FLA",
        "Subject_Code":"CSE411",
        "Section":"B",
        "Semester":"Odd",
        "Number_of_Students":20,
        "Number_of_COs":4}
    

    # Component_Details={"P1_I":7,
    #                     "CA_I":4,
    #                     "EndSem_E":13}

    Component_Details={"P1_I":7,
                        "CA_I":4,
                        "EndSem_E":13}

    # Component_Details={"P1_I":{"Number_of_questions":3},
    #                     "EndSem_E":{"Number_of_questions":3}}

    output_dir='C:\\Users\\raman\\OneDrive - Amrita vishwa vidyapeetham\\ASE\\Projects\\NBA\\NBA_v3\\dev_19.1\\flux\\nba\\Part_1\\TestFiles'
    file_name=driver_part1(data,Component_Details, output_dir)
    #open file
    os.system('"' + os.path.join(output_dir, file_name) + '"')    