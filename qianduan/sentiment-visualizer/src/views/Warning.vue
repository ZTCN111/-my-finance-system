<template>
  <el-card>
    <h2 style="margin-bottom: 20px;">风险预警记录</h2>

    <el-table :data="warningData" border style="width: 100%">
      <el-table-column prop="keyword" label="关键词" />
      <el-table-column prop="type" label="预警类型" />
      <el-table-column prop="platform" label="涉及平台" />
      <el-table-column prop="time" label="预警时间" width="160" />
      <el-table-column prop="level" label="危险等级" width="120">
        <template #default="{ row }">
          <el-tag
            :type="row.level === '高' ? 'danger' : row.level === '中' ? 'warning' : 'info'"
          >
            {{ row.level }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const warningData = ref([]);

const fetchWarnings = async () => {
  try {
    const res = await api.get('/api/warning/list');
    warningData.value = res.data;
  } catch (error) {
    console.error('获取预警记录失败:', error);
  }
}

onMounted(() => {
  fetchWarnings();
})
</script>