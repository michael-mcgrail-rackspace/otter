"""
Test to create and verify get and list group.
"""
from test_repo.autoscale.fixtures import AutoscaleFixture


class ScalingGroupListTest(AutoscaleFixture):

    """
    Verify get and list group.
    """

    @classmethod
    def setUpClass(cls):
        """
        Create a scaling group.
        """
        super(ScalingGroupListTest, cls).setUpClass()
        first_group = cls.autoscale_behaviors.create_scaling_group_min()
        cls.first_scaling_group = first_group.entity
        second_group = cls.autoscale_behaviors.create_scaling_group_min()
        cls.second_scaling_group = second_group.entity
        third_group = cls.autoscale_behaviors.create_scaling_group_min()
        cls.third_scaling_group = third_group.entity
        cls.resources.add(cls.first_scaling_group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.resources.add(cls.second_scaling_group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.resources.add(cls.third_scaling_group.id,
                          cls.autoscale_client.delete_scaling_group)

    def test_get_scaling_group(self):
        """
        Verify the get group for response code 200, headers and data.
        """
        group_info_response = self.autoscale_client.\
            view_manifest_config_for_scaling_group(
                group_id=self.first_scaling_group.id)
        group_info = group_info_response.entity
        self.assertEqual(200, group_info_response.status_code,
                         msg='The get scaling group call failed with {0} for group'
                         ' {1}'.format(group_info_response.status_code,
                                       self.first_scaling_group.id))
        self.validate_headers(group_info_response.headers)
        self.assertEqual(group_info.id, self.first_scaling_group.id,
                         msg='Group id did not match for group '
                         '{0}'.format(self.first_scaling_group.id))
        self.assertEqual(group_info.groupConfiguration.name,
                         self.first_scaling_group.groupConfiguration.name,
                         msg='Group name did not match for group '
                         '{0}'.format(self.first_scaling_group.id))
        self.assertEqual(group_info.groupConfiguration.minEntities,
                         self.first_scaling_group.groupConfiguration.minEntities,
                         msg="Group's minimum entities did not match for group "
                         "{0}".format(self.first_scaling_group.id))
        self.assertEqual(group_info.launchConfiguration,
                         self.first_scaling_group.launchConfiguration,
                         msg="Group's launch configurations did not match for group "
                         '{0}'.format(self.first_scaling_group.id))

    def test_default_maxentities_set_on_a_group(self):
        """
        Verify the default max entities set on a group when max enetities are
        not specified by the user, when creating group.
        """
        for each_group in [self.first_scaling_group, self.second_scaling_group]:
            group_info = self.autoscale_client.\
                view_manifest_config_for_scaling_group(
                    group_id=each_group.id).entity
            self.assertEquals(
                group_info.groupConfiguration.maxEntities, self.max_maxentities,
                msg='The maxentities set by default on the group {0} should be {1} '
                ' but is {2}'.format(each_group.id, self.max_maxentities,
                                     group_info.groupConfiguration.maxEntities))

    def test_list_scaling_group(self):
        """
        Verify the list group for response code 200, headers and data.
        """
        list_groups_response = self.autoscale_client.list_scaling_groups()
        list_groups = list_groups_response.entity
        self.assertEqual(200, list_groups_response.status_code,
                         msg='The list scaling group call failed with: '
                         '{0}'.format(list_groups_response.content))
        self.validate_headers(list_groups_response.headers)
        group_id_list = []
        for i in list_groups:
            group_id_list.append(i.id)
        self.assertTrue(self.first_scaling_group.id in
                        group_id_list, msg='Group with id {0} was not found in the list '
                        '{1}'.format(self.first_scaling_group.id, group_id_list))
        self.assertTrue(self.second_scaling_group.id in
                        group_id_list, msg='Group with id {0} was not found in the list '
                        '{1}'.format(self.second_scaling_group.id, group_id_list))
        self.assertTrue(self.third_scaling_group.id in
                        group_id_list, msg='Group with id {0} was not found in the list '
                        '{1}'.format(self.third_scaling_group.id, group_id_list))
