import boto3
from datetime import datetime, timezone, timedelta

client = boto3.client('ec2')

def lambda_handler(event, context):

    # --- CLEAN UP UNUSED EBS VOLUMES ---
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']

    for vol in volumes:
        volume_id = vol['VolumeId']
        try:
            ec2.delete_volume(VolumeId=volume_id)
            print(f"Deleted unused EBS volume: {volume_id}")
        except Exception as e:
            print(f"Error deleting volume {volume_id}: {str(e)}")

    # --- CLEAN UP OLD SNAPSHOTS (optional) ---
    days_old = 30
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)

    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    for snap in snapshots:
        snap_id = snap['SnapshotId']
        start_time = snap['StartTime']

        if start_time < cutoff:
            try:
                ec2.delete_snapshot(SnapshotId=snap_id)
                print(f"Deleted old snapshot: {snap_id}")
            except Exception as e:
                print(f"Error deleting snapshot {snap_id}: {str(e)}")

    return {"status": "cleanup completed"}
