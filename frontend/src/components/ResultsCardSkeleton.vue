<template>
  <!-- The container for the skeleton card -->
  <div class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 min-h-[300px] w-full">
    <!-- The animate-pulse class from Tailwind CSS -->
    <div class="animate-pulse">

      <!-- Skeleton for the Header (Country Name) -->
      <div class="h-8 bg-slate-700 rounded w-1/2 mb-6"></div>

      <!-- for the list items -->
      <div class="space-y-4">

        <!-- for a single data row -->
        <div class="flex justify-between items-center">
          <div class="h-4 bg-slate-700 rounded w-2/5"></div>
          <div class="h-6 bg-slate-700 rounded w-1/3"></div>
        </div>

        <!-- for another data row -->
        <div class="flex justify-between items-center">
          <div class="h-4 bg-slate-700 rounded w-1/2"></div>
          <div class="h-6 bg-slate-700 rounded w-1/4"></div>
        </div>

        <!-- ... and another ... -->
        <div class="flex justify-between items-center">
          <div class="h-4 bg-slate-700 rounded w-2/5"></div>
          <div class="h-6 bg-slate-700 rounded w-1/3"></div>
        </div>

        <!-- for the AI Chirp sections -->
        <div class="pt-4 mt-4 border-t border-white/10">
            <div class="h-4 bg-slate-700 rounded w-1/4 mb-2"></div>
            <div class="h-3 bg-slate-700 rounded w-full"></div>
            <div class="h-3 bg-slate-700 rounded w-5/6 mt-1"></div>
        </div>

      </div>
    </div>
  </div>
</template>