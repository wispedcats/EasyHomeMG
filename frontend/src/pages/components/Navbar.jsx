export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 transition-all duration-300 bg-slate-700/20 backdrop-blur-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-4 lg:px-8">
        <div className="flex justify-between items-center h-14 sm:h-16 md:h-20">
          <div className="flex items-center space-x-1">
            <div>
              <img src="/HomeServerMG.svg" alt="Logo" />
            </div>
            <div>
              <span className="text-red-300 font-mono">EasyHome</span>
              <span className="text-slate-200 font-mono">MG</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <a href="/dashboard" className="text-md text-white hover:text-slate-400">Open Dashboard</a>
          </div>
        </div>
      </div>
    </nav>
  );
}
