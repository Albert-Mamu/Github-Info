#!/usr/bin/env python3
"""
GitHub Repository Traffic Analyzer
Created by: Albert Sandro Mamu
Module: GITHUB-INTEL
Description: Advanced tool untuk memantau views, clones, dan traffic analytics repo GitHub
"""

import requests
import json
import datetime
import pandas as pd
from typing import Dict, List, Optional
import argparse
import sys

class GitHubTrafficAnalyzer:
    def __init__(self, token: str, owner: str, repo: str):
        """
        Initialize GitHub Traffic Analyzer
        
        Args:
            token: GitHub Personal Access Token
            owner: Repository owner username
            repo: Repository name
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Internal method untuk membuat request ke GitHub API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error accessing {endpoint}: {e}")
            return None
    
    def get_views_traffic(self) -> Optional[Dict]:
        """Mendapatkan data views traffic (14 hari terakhir)"""
        return self._make_request("/traffic/views")
    
    def get_clones_traffic(self) -> Optional[Dict]:
        """Mendapatkan data clones traffic (14 hari terakhir)"""
        return self._make_request("/traffic/clones")
    
    def get_referral_sources(self) -> Optional[Dict]:
        """Mendapatkan data referral sources (sumber traffic)"""
        return self._make_request("/traffic/popular/referrers")
    
    def get_popular_paths(self) -> Optional[Dict]:
        """Mendapatkan path/file paling populer"""
        return self._make_request("/traffic/popular/paths")
    
    def get_repo_info(self) -> Optional[Dict]:
        """Mendapatkan informasi dasar repository"""
        return self._make_request("")
    
    def analyze_traffic_trends(self, views_data: Dict, clones_data: Dict) -> Dict:
        """Analisis mendalam trends traffic"""
        if not views_data or not clones_data:
            return {}
            
        views = views_data.get('views', [])
        clones = clones_data.get('clones', [])
        
        # Calculate totals
        total_views = sum(item['count'] for item in views)
        total_uniques = sum(item['uniques'] for item in views)
        total_clones = sum(item['count'] for item in clones)
        total_clones_uniques = sum(item['uniques'] for item in clones)
        
        # Calculate daily averages
        avg_views = total_views / len(views) if views else 0
        avg_clones = total_clones / len(clones) if clones else 0
        
        # Find peak days
        peak_views_day = max(views, key=lambda x: x['count']) if views else {}
        peak_clones_day = max(clones, key=lambda x: x['count']) if clones else {}
        
        return {
            'total_views': total_views,
            'total_unique_visitors': total_uniques,
            'total_clones': total_clones,
            'total_unique_cloners': total_clones_uniques,
            'average_daily_views': round(avg_views, 2),
            'average_daily_clones': round(avg_clones, 2),
            'peak_views_day': peak_views_day,
            'peak_clones_day': peak_clones_day,
            'analysis_period_days': len(views)
        }
    
    def generate_report(self, detailed: bool = False) -> Dict:
        """Generate comprehensive traffic report"""
        print("🔄 Collecting GitHub repository traffic data...")
        
        # Collect all data
        views_data = self.get_views_traffic()
        clones_data = self.get_clones_traffic()
        referrals = self.get_referral_sources()
        paths = self.get_popular_paths()
        repo_info = self.get_repo_info()
        
        # Analyze trends
        trends = self.analyze_traffic_trends(views_data, clones_data)
        
        report = {
            'repository_info': {
                'name': repo_info.get('full_name') if repo_info else f"{self.owner}/{self.repo}",
                'description': repo_info.get('description', 'No description'),
                'stars': repo_info.get('stargazers_count', 0) if repo_info else 0,
                'forks': repo_info.get('forks_count', 0) if repo_info else 0,
                'watchers': repo_info.get('watchers_count', 0) if repo_info else 0
            },
            'traffic_summary': trends,
            'referral_sources': referrals or [],
            'popular_paths': paths or []
        }
        
        if detailed and views_data:
            report['detailed_views'] = views_data.get('views', [])
            report['detailed_clones'] = clones_data.get('clones', [])
        
        return report
    
    def display_report(self, report: Dict):
        """Display formatted report"""
        print("\n" + "="*70)
        print("🚀 GITHUB REPOSITORY TRAFFIC ANALYTICS REPORT")
        print("Created By Albert Mamu\n")
        print("If you like this development, you can donate a little help to the :")
        print("PayPal : albertflicky@gmail.com")
        print("Bitcoin : bc1qxmr748pd90add7nxyjpml9h2q5dl9z8yq0vkq5")
        print("Solana (SOL) : 5EcfHby6qW3ko5a54YMdMxDgVU9e952JDgeDd9Ec22iU\n")
        print("0xd738177A1dFF20CBE27BD6aFc23A38C40988a5a1")

        print("="*70)
        
        # Repository Info
        repo_info = report['repository_info']
        print(f"\n📁 REPOSITORY: {repo_info['name']}")
        print(f"📝 Description: {repo_info['description']}")
        print(f"⭐ Stars: {repo_info['stars']} | 🍴 Forks: {repo_info['forks']} | 👁️ Watchers: {repo_info['watchers']}")
        
        # Traffic Summary
        traffic = report['traffic_summary']
        print(f"\n📊 TRAFFIC SUMMARY (Last {traffic.get('analysis_period_days', 14)} days):")
        print(f"👀 Total Views: {traffic.get('total_views', 0):,}")
        print(f"👥 Unique Visitors: {traffic.get('total_unique_visitors', 0):,}")
        print(f"📥 Total Clones: {traffic.get('total_clones', 0):,}")
        print(f"👤 Unique Cloners: {traffic.get('total_unique_cloners', 0):,}")
        print(f"📈 Average Daily Views: {traffic.get('average_daily_views', 0):.1f}")
        print(f"📥 Average Daily Clones: {traffic.get('average_daily_clones', 0):.1f}")
        
        # Peak days
        peak_views = traffic.get('peak_views_day', {})
        peak_clones = traffic.get('peak_clones_day', {})
        if peak_views:
            print(f"📅 Peak Views Day: {peak_views.get('timestamp', 'N/A')} - {peak_views.get('count', 0)} views")
        if peak_clones:
            print(f"📅 Peak Clones Day: {peak_clones.get('timestamp', 'N/A')} - {peak_clones.get('count', 0)} clones")
        
        # Referral Sources
        referrals = report.get('referral_sources', [])
        if referrals:
            print(f"\n🔗 TOP REFERRAL SOURCES:")
            for i, ref in enumerate(referrals[:5], 1):
                print(f"  {i}. {ref.get('referrer', 'Unknown')}: {ref.get('count', 0):,} views, {ref.get('uniques', 0):,} uniques")
        
        # Popular Paths
        paths = report.get('popular_paths', [])
        if paths:
            print(f"\n📂 MOST POPULAR PATHS:")
            for i, path in enumerate(paths[:5], 1):
                print(f"  {i}. {path.get('title', 'No title')}")
                print(f"     Path: {path.get('path', 'N/A')}")
                print(f"     Views: {path.get('count', 0):,}, Unique: {path.get('uniques', 0):,}")
        
        print("\n" + "="*70)
        print("✅ Thank you for using this software")
        print("="*70)

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='GitHub Repository Traffic Analyzer')
    parser.add_argument('--token', required=True, help='GitHub Personal Access Token')
    parser.add_argument('--owner', required=True, help='Repository owner username')
    parser.add_argument('--repo', required=True, help='Repository name')
    parser.add_argument('--detailed', action='store_true', help='Show detailed daily data')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = GitHubTrafficAnalyzer(args.token, args.owner, args.repo)
    
    # Generate and display report
    report = analyzer.generate_report(detailed=args.detailed)
    analyzer.display_report(report)
    
    # Save to JSON file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"github_traffic_{args.owner}_{args.repo}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Report saved to: {filename}")

if __name__ == "__main__":
    # Example usage if run directly
    if len(sys.argv) == 1:
        print("🚀 GitHub Traffic Analyzer - Manual Mode")
        print("Enter your GitHub credentials:")
        
        token = input("GitHub Token: ").strip()
        owner = input("Repository Owner: ").strip()
        repo = input("Repository Name: ").strip()
        
        if token and owner and repo:
            analyzer = GitHubTrafficAnalyzer(token, owner, repo)
            report = analyzer.generate_report(detailed=True)
            analyzer.display_report(report)
        else:
            print("❌ Missing required information!")
            print("\nUsage example:")
            print("python github_traffic.py --token YOUR_TOKEN --owner username --repo reponame")
    else:
        main()