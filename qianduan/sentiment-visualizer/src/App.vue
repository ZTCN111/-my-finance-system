<template>
  <el-container style="height: 100vh">
    <el-aside width="200px">
      <el-menu router default-active="/dashboard">
        <el-menu-item index="/dashboard">舆情总览</el-menu-item>
        <el-menu-item index="/analysis">情绪分析</el-menu-item>
        <el-menu-item index="/warning">风险预警</el-menu-item>
      </el-menu>
    </el-aside>

    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import 'element-plus/dist/index.css'
</script>