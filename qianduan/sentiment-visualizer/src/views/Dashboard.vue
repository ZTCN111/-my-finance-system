<template>
  <el-card>
    <h2 style="margin-bottom: 20px;">帖子可视化总览</h2>
    <p style="margin-bottom: 10px; color: #666; font-size: 14px;">
      📌 情绪指数是根据每日所有帖子情感分析平均得出，范围 0~1。&gt;0.7 表示乐观，0.4~0.7 中性，&lt;0.4 偏悲观。
    </p>

    <div style="margin-bottom: 20px; display: flex; align-items: center;">
      <el-input
        v-model="searchInput"
        placeholder="输入股票代码（默认为000001）"
        clearable
        style="width: 300px; margin-right: 10px;"
        @keyup.enter="handleSearch"
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>

      <el-tooltip
        class="item"
        effect="dark"
        content="📌 情绪指数说明：基于每日所有相关帖子情感分析得出的平均分，范围 0~1。0.7~1 表示乐观，0.4~0.7 中性，0~0.4 偏悲观，用于衡量市场对该股票的整体情绪。"
        placement="right"
      >
        <el-icon style="margin-left: 10px; cursor: pointer;">
          <el-icon-question-filled />
        </el-icon>
      </el-tooltip>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <div ref="lineChart" style="width: 100%; height: 400px;"></div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <div ref="wordCloudChart" style="width: 100%; height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
    <p style="margin-top: 10px; text-align: center; font-weight: bold;">当前股票代码：{{ searchInput }}</p>
  </el-card>
</template>

<script setup>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const lineChart = ref(null)
const wordCloudChart = ref(null)
const posts = ref([])
const postDates = ref([])
const postScores = ref([])
const wordList = ref([])
const searchInput = ref('000001')

const fetchData = async (code) => {
  try {
    const params = {}
    if (code && code.trim() !== '') params.code = code.trim()
    const res = await axios.get('http://127.0.0.1:5000/api/post/list', { params })
    posts.value = res.data.data || []
    console.log('✅ 拉取到帖子数据：', posts.value)
    if (!posts.value.length) return

    posts.value.sort((a, b) => (a.date > b.date ? 1 : -1))
    processLineChartData()
    processWordCloudData()
    renderCharts()
  } catch (error) {
    console.error('❌ 获取数据失败', error)
  }
}

const processLineChartData = () => {
  const dateMap = {}
  for (const p of posts.value) {
    const key = p.date || '未知'
    if (!dateMap[key]) dateMap[key] = []
    dateMap[key].push(p.score || 0.5)
  }
  postDates.value = Object.keys(dateMap).sort()
  postScores.value = postDates.value.map(date => {
    const scores = dateMap[date]
    return Number((scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(3))
  })
}

const processWordCloudData = () => {
  const wordCount = {}
  for (const p of posts.value) {
    const words = (p.title?.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, ' ') || '').split(/\s+/)
    for (const w of words) {
      if (w.length > 1) wordCount[w] = (wordCount[w] || 0) + 1
    }
  }
  wordList.value = Object.entries(wordCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
    .map(([name, value]) => ({ name, value }))
}

const renderCharts = () => {
  if (lineChart.value) {
    const line = echarts.init(lineChart.value)
    line.setOption({
      title: { text: '个股每日情绪指数走势' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: postDates.value },
      yAxis: { type: 'value', min: 0, max: 1 },
      series: [{
        data: postScores.value,
        type: 'line',
        smooth: true,
        areaStyle: {},
      }]
    })
  }

  if (wordCloudChart.value) {
    const cloud = echarts.init(wordCloudChart.value)
    cloud.setOption({
      title: { text: `关键词词云` },
      tooltip: {
        trigger: 'item',
        formatter: item => `${item.name} : ${item.value}`
      },
      series: [{
        type: 'wordCloud',
        shape: 'circle',
        gridSize: 10,
        sizeRange: [12, 50],
        rotationRange: [-90, 90],
        textStyle: {
          normal: {
            color: () => `hsl(${Math.random() * 360}, 100%, 60%)`,
          },
        },
        data: wordList.value,
      }]
    })
  }
}

const handleSearch = async () => {
  await fetchData(searchInput.value || '000001')
  if (!posts.value.length) {
    ElMessage.warning('没有查询到该股票代码的帖子数据')
  }
}

onMounted(() => {
  fetchData('000001')
})
</script>

<style scoped>
</style>