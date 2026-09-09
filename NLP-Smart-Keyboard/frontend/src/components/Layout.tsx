import { Link, Outlet, useLocation } from 'react-router-dom';
import { Keyboard, Activity, Database, LayoutDashboard } from 'lucide-react';

export default function Layout() {
  const location = useLocation();
  
  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Smart Keyboard Demo', path: '/demo', icon: <Keyboard size={20} /> },
    { name: 'NLP Analyzer', path: '/analyzer', icon: <Activity size={20} /> },
    { name: 'Dataset & Scraper', path: '/data', icon: <Database size={20} /> },
  ];

  return (
    <div className="flex h-screen bg-background text-foreground dark:bg-gray-900 dark:text-white transition-colors duration-200">
      <aside className="w-64 border-r border-border dark:border-gray-800 bg-card dark:bg-gray-950 flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-emerald-400 bg-clip-text text-transparent flex items-center gap-2">
            <Keyboard className="text-primary" /> NeuroKey
          </h1>
          <p className="text-xs text-gray-500 mt-1">NLP Smart Keyboard Platform</p>
        </div>
        
        <nav className="flex-1 px-4 space-y-2 mt-4">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive 
                    ? 'bg-primary/10 text-primary font-medium shadow-sm' 
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'
                }`}
              >
                {item.icon}
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-border dark:border-gray-800">
          <div className="text-xs text-center text-gray-400">
            NeuroKey v1.0.0
          </div>
        </div>
      </aside>
      
      <main className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-900 p-8">
        <Outlet />
      </main>
    </div>
  );
}
