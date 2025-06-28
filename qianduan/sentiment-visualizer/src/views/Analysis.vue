<template>
  <el-card>
    <h2 style="margin-bottom: 20px;">帖子信息总览</h2>

    <div style="margin-bottom: 20px; display: flex; align-items: center;">
      <el-input
        v-model="searchCode"
        placeholder="输入股票代码（默认000001）"
        style="width: 300px; margin-right: 10px;"
        clearable
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="handleClear">重置</el-button>
    </div>

    <el-table
      :data="tableData"
      border
      style="width: 100%"
      :header-cell-style="{ textAlign: 'center' }"
      :cell-style="{ textAlign: 'center' }"
    >
      <el-table-column prop="code" label="股票代码" width="100" show-overflow-tooltip />
      <el-table-column prop="title" label="帖子标题" min-width="200">
        <template #default="{ row }">
          <el-tooltip effect="dark" placement="top" :content="row.title">
            <span class="ellipsis">{{ row.title }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="author" label="作者" width="120">
        <template #default="{ row }">
          <el-tooltip effect="dark" placement="top" :content="row.author">
            <span class="ellipsis">{{ row.author }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="view" label="浏览数" width="80" />
      <el-table-column prop="comment_num" label="评论数" width="80" />
      <el-table-column prop="date" label="日期" width="110" />
      <el-table-column prop="time" label="时间" width="90" />
      <el-table-column prop="url" label="帖子链接" min-width="200">
        <template #default="{ row }">
          <el-tooltip effect="dark" placement="top" :content="row.url">
            <a :href="row.url" target="_blank" class="ellipsis">{{ row.url }}</a>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="sentiment" label="情绪判断" width="140" />
      <el-table-column prop="score" label="情绪评分" width="100">
        <template #default="{ row }">
          {{ row.score ? row.score.toFixed(2) : '-' }}
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top: 20px; text-align: right;">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const tableData = ref([]);
const searchCode = ref('000001');     // 默认股票代码
const currentPage = ref(1);
const pageSize = 10;
const total = ref(0);

const fetchPosts = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    };
    if (searchCode.value.trim() !== '') {
      params.code = searchCode.value.trim();
    }

    const res = await api.get('/api/post/list', { params });
    tableData.value = res.data.data;
    total.value = res.data.total;
    console.log('✅ 拉取数据成功:', res.data);
  } catch (error) {
    console.error('❌ 拉取数据失败:', error);
  }
};

const handlePageChange = (page) => {
  currentPage.value = page;
  fetchPosts();
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchPosts();
};

const handleClear = () => {
  searchCode.value = '000001';
  currentPage.value = 1;
  fetchPosts();
};

onMounted(() => {
  fetchPosts();
});
</script>

<style scoped>
.ellipsis {
  display: inline-block;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
}

:deep(.custom-tooltip .el-tooltip__popper) {
  max-width: none;
  width: auto;
  min-width: 300px;
  white-space: normal;
  word-break: break-all;
  overflow-wrap: break-word;
  line-height: 1.4;
  padding: 10px;
  font-size: 14px;
}
</style>