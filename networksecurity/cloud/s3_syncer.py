import os


class S3Sync:
    # upload folder to s3
    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str):
        # Placeholder for actual S3 sync logic
        command=f"aws s3 sync {folder} {aws_bucket_url}"
        os.system(command)
    
    # get folder from s3 to local
    def sync_folder_from_s3(self, aws_bucket_url: str, folder: str):
        # Placeholder for actual S3 sync logic
        command=f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command)