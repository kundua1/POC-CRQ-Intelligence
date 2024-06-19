create table Ongoing_Patch_CRQ_Info(
	id int not null primary key identity(1,1),
	Time_Stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	CRQ_Number nvarchar(100),
	Start_Date_Time nvarchar(100),
	End_Date_Time nvarchar(100),
	Change_Asset_Group nvarchar(100),
	Windows_Server_Count nvarchar(100),
	Windows_Exception_Count nvarchar(100),
	Unix_Server_Count nvarchar(100),
    Unix_Exception_Count nvarchar(100)
)
