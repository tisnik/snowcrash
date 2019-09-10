# Table Errors:
    - Language - It's a File Language (VARCHAR NOT NULL)
    - Type - It's a Error type's name (VARCHAR NOT NULL)
    - Path - It's a Fill Path of error (VARCHAR NULL) 
    - Line - It's a Line of error (INT NULL)
    - MSG - It's a Message of error (VARCHAR NULL)
    - First - It's a First time of error record (YYYY-MM-DD HH-MM-SS NULL) 
    - Last - It's a Last time of error record (YYYY-MM-DD HH-MM-SS NULL) 
# Table Type:
    - Language - It's a Error Language (VARCHAR NOT NULL)
    - TypeName - It's a Error type (VARCHAR NOT NULL)
    - MSG - It's a Moustly use message (VARCHAR) NULL
# Table Language:
    - Language - It's a Name of programing language (VARCHAR NOT NULL)
    - Regex - It's a string to recognition File (VARCHAR NOT NULL)
# Table Solution: 
    - Language - It's a File Language (VARCHAR NOT NULL)
    - Type - It's a Error type's name (VARCHAR NOT NULL)
    - Priority - It's a Priority to use Soulution, it's 1(First Use) to 999(Last Use) (INT NOT NULL)      
    - Solution - It's a Solution of error (VARCHAR NOT NULL)
