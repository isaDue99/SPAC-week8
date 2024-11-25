-- Table for products
CREATE TABLE IF NOT EXISTS products (
    ID INT AUTO_INCREMENT,
    -- The class name of the Python dataclass
    Type VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Description VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    LastUpdatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pkProductId PRIMARY KEY (ID),
    CONSTRAINT uqName UNIQUE(name)
);

-- Table for dynamic product attributes
CREATE TABLE IF NOT EXISTS product_attributes (
    ProductID INT,
    AttributeName VARCHAR(255) NOT NULL,
    AttributeValue VARCHAR(255) NOT NULL,
    CONSTRAINT fkProductId FOREIGN KEY (ProductID) REFERENCES products(ID),
    -- Make sure there is only one unique paring of the product id and attribute name.
    CONSTRAINT uqProductAttribute UNIQUE (ProductID, AttributeName)
);