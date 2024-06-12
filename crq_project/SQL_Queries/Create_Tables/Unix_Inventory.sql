create table Unix_Inventory(
	id int not null primary key identity(1,1),
	Time_Stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FQDN nvarchar(100),
	IP_Address nvarchar(100),
	Trust_Level nvarchar(100),
	Operating_System nvarchar(100),
	Business_Unit nvarchar(100),
	Application_Name nvarchar(100),
	Application_Owner nvarchar(100),
	Asset_Group_Classification nvarchar(100),
	Last_Patch_Date nvarchar(100),
	Upcoming_Patch_Schedule nvarchar(100),
	Cyber_Exception nvarchar(100),
	Cyber_REQ nvarchar(100),
	Exception_Approval_Attachment nvarchar(100),
	Patch_CRQ nvarchar(100)
)
