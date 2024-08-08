from typing import Dict, Any, List

from ..data.feature import FeatureData
from ..objects.feature import Feature

from ..clients import yaml as yaml_client


class FeatureRepository(object):

    def exists(self, id: str) -> bool:
        raise NotImplementedError()
    
    def get(self, id: str) -> Feature:
        raise NotImplementedError()
    
    def save(self, feature: Feature):
        raise NotImplementedError()


class YamlRepository(FeatureRepository):

    def __init__(self, feature_yaml_base_path: str):
        self.base_path = feature_yaml_base_path

    def exists(self, id: str) -> bool:

        # Retrieve the feature by id.
        feature = self.get(id)

        # Return whether the feature exists.
        return feature is not None

    def get(self, id: str) -> Feature:

        # Get context group and feature key from the id.
        group_id, feature_key = id.split('.')
        
        # Load feature data from yaml.
        _data: FeatureData = yaml_client.load(
            self.base_path,
            create_data=lambda data: FeatureData.from_yaml_data(id=id, group_id=group_id, **data),
            start_node=lambda data: data.get('features').get('groups').get(group_id).get('features').get(feature_key)
        )

        # Return None if feature data is not found.
        if not _data:
            return None
        
        # Return feature.
        return _data.map('to_object.yaml')
    
    def save(self, feature: Feature):
            
            # Create updated feature data.
            feature_data = FeatureData.new(**feature.to_primitive())
    
            # Update the feature data.
            yaml_client.save(
                path=self.base_path,
                data=feature_data,
                data_save_path=f'features.groups.{feature.group_id}.features.{feature_data.feature_key}'
            )
    
            # Return the updated feature object.
            return feature_data.map('to_object.yaml')
