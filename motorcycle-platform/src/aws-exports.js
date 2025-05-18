const awsConfig = {
  Auth: {
    region: "ap-southeast-1", // AWS region
    userPoolId: "ap-southeast-1_jHKYEhIzj", // Cognito User Pool ID
    userPoolWebClientId: "4pgoe8g867o22jffprb1hgme8u", // Cognito App Client ID
  },
  Storage: {
    bucket: "fyp-a03-images", // S3 bucket for file uploads
    region: "ap-southeast-1", // S3 bucket region
  },
  DynamoDB: {
    tableName: "ProductListings", // DynamoDB table name
    region: "ap-southeast-1", // DynamoDB region
  },
};

export default awsConfig;