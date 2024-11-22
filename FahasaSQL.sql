USE Fahasa;
GO
-- Thêm khóa chính cho bảng publisher
ALTER TABLE publisher
ADD CONSTRAINT PK_Publisher PRIMARY KEY (PublisherID);

-- Thêm khóa chính cho bảng author
ALTER TABLE author
ADD CONSTRAINT PK_Author PRIMARY KEY (AuthorID);

-- Thêm khóa chính cho bảng supplier
ALTER TABLE supplier
ADD CONSTRAINT PK_Supplier PRIMARY KEY (SupplierID);

-- Thêm khóa chính cho bảng level
ALTER TABLE level
ADD CONSTRAINT PK_Level PRIMARY KEY (LevelID);

-- Thêm khóa chính cho bảng grade
ALTER TABLE grade
ADD CONSTRAINT PK_Grade PRIMARY KEY (GradeID);

-- Thêm khóa chính cho bảng book
ALTER TABLE book
ADD CONSTRAINT PK_Book PRIMARY KEY (BookID);

-- Thêm khóa ngoại PublisherID tham chiếu đến bảng publisher
ALTER TABLE book
ADD CONSTRAINT FK_Book_Publisher
FOREIGN KEY (PublisherID)
REFERENCES publisher(PublisherID);

-- Thêm khóa ngoại AuthorID tham chiếu đến bảng author
ALTER TABLE book
ADD CONSTRAINT FK_Book_Author
FOREIGN KEY (AuthorID)
REFERENCES author(AuthorID);

-- Thêm khóa ngoại SupplierID tham chiếu đến bảng supplier
ALTER TABLE book
ADD CONSTRAINT FK_Book_Supplier
FOREIGN KEY (SupplierID)
REFERENCES supplier(SupplierID);

-- Thêm khóa ngoại LevelID tham chiếu đến bảng level
ALTER TABLE book
ADD CONSTRAINT FK_Book_Level
FOREIGN KEY (LevelID)
REFERENCES level(LevelID);

-- Thêm khóa ngoại GradeID tham chiếu đến bảng grade
ALTER TABLE book
ADD CONSTRAINT FK_Book_Grade
FOREIGN KEY (GradeID)
REFERENCES grade(GradeID);
