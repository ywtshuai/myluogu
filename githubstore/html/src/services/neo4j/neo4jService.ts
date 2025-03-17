/**
 * @file Neo4j 数据库服务
 * @description 提供与 Neo4j 图数据库的连接和操作
 */
import neo4j, { Driver, Session, Record as Neo4jRecord } from 'neo4j-driver';

// 定义模拟记录类型
interface MockRecord {
  get: (key: string) => any;
  toObject: () => Record<string, any>;
}

// 添加 Neo4j 错误类型定义
interface Neo4jError extends Error {
  code?: string;
  name: string;
}

class Neo4jService {
  private driver: Driver | null = null;
  private static instance: Neo4jService;
  private mockMode: boolean = false;
  private isConnecting: boolean = false;
  private connectionRetryCount: number = 0;
  private readonly MAX_RETRY_COUNT = 3;
  private readonly RETRY_DELAY = 1000; // 1秒

  private constructor() {}

  public static getInstance(): Neo4jService {
    if (!Neo4jService.instance) {
      Neo4jService.instance = new Neo4jService();
    }
    return Neo4jService.instance;
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  public async connect(uri: string, username: string, password: string): Promise<void> {
    if (this.isConnecting) {
      console.log('已有连接正在进行中，跳过...');
      return;
    }

    this.isConnecting = true;

    try {
      console.log('开始尝试连接 Neo4j 数据库...');
      console.log('连接参数:', { uri, username, passwordLength: password.length });

      // 如果已经有连接，先关闭
      if (this.driver) {
        console.log('检测到现有连接，准备关闭...');
        await this.close();
        // 添加短暂延迟确保连接完全关闭
        await this.delay(500);
      }
      
      // 创建新连接
      console.log('创建新的数据库连接...');
      this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password), {
        maxConnectionLifetime: 3 * 60 * 60 * 1000, // 3小时
        maxConnectionPoolSize: 50,
        connectionAcquisitionTimeout: 2000, // 连接获取超时时间
        maxTransactionRetryTime: 30000, // 30秒事务重试时间
      });
      
      // 验证连接
      console.log('验证连接可用性...');
      try {
        await this.driver.verifyConnectivity();
        console.log('Neo4j 数据库连接验证成功');
        this.mockMode = false;
        this.connectionRetryCount = 0; // 重置重试计数
      } catch (error) {
        const verifyError = error as Neo4jError;
        console.error('连接验证失败:', {
          error: verifyError,
          message: verifyError.message,
          code: verifyError.code,
          stack: verifyError.stack
        });

        // 清理失败的连接
        if (this.driver) {
          await this.driver.close();
          this.driver = null;
        }

        throw verifyError;
      }

    } catch (error) {
      const neo4jError = error as Neo4jError;
      console.error('Neo4j 数据库连接失败:', {
        error: neo4jError,
        message: neo4jError.message,
        code: neo4jError.code,
        name: neo4jError.name,
        stack: neo4jError.stack
      });
      
      this.driver = null;
      this.mockMode = true;
      
      // 如果还有重试机会，则尝试重连
      if (this.connectionRetryCount < this.MAX_RETRY_COUNT) {
        console.log(`准备进行第 ${this.connectionRetryCount + 1} 次重试...`);
        this.isConnecting = false;
        await this.delay(this.RETRY_DELAY);
        return this.connect(uri, username, password);
      }
      
      console.log('启用模拟模式');
    } finally {
      this.isConnecting = false;
    }
  }

  public async executeQuery(query: string, params: Record<string, any> = {}): Promise<Neo4jRecord[] | MockRecord[]> {
    console.log('执行查询:', {
      query,
      params,
      mockMode: this.mockMode,
      hasDriver: !!this.driver,
      driverState: this.driver ? 'active' : 'null'
    });

    if (this.mockMode) {
      console.log('模拟模式: 跳过查询执行');
      return [];
    }

    if (!this.driver) {
      console.error('数据库连接未初始化');
      throw new Error('Neo4j 数据库未连接');
    }

    let session: Session | null = null;
    let retryCount = 0;
    const maxRetries = 3;

    while (retryCount < maxRetries) {
      try {
        if (session) {
          await session.close();
          session = null;
        }
        
        session = this.driver.session();
        console.log('开始执行查询...');
        const result = await session.run(query, params);
        console.log('查询执行成功，返回记录数:', result.records.length);
        return result.records;
      } catch (error) {
        const queryError = error as Neo4jError;
        console.error(`查询执行失败 (尝试 ${retryCount + 1}/${maxRetries}):`, {
          error: queryError,
          message: queryError.message,
          code: queryError.code,
          stack: queryError.stack
        });

        retryCount++;
        
        if (queryError.code === 'ServiceUnavailable' || queryError.message.includes('Pool is closed')) {
          console.log('检测到连接池关闭，尝试重新初始化连接...');
          await this.delay(1000);
          continue;
        }

        throw queryError;
      } finally {
        if (session) {
          try {
            console.log('关闭会话...');
            await session.close();
          } catch (closeError) {
            console.error('关闭会话时出错:', closeError);
          }
          session = null;
        }
      }
    }

    throw new Error(`查询失败，已重试 ${maxRetries} 次`);
  }

  public async close(): Promise<void> {
    if (this.driver) {
      try {
        console.log('开始关闭数据库连接...');
        await this.driver.close();
        this.driver = null;
        console.log('Neo4j 数据库连接已成功关闭');
      } catch (error) {
        const closeError = error as Neo4jError;
        console.error('关闭 Neo4j 连接失败:', {
          error: closeError,
          message: closeError.message,
          code: closeError.code,
          stack: closeError.stack
        });
        this.driver = null;
      }
    } else {
      console.log('没有活动的数据库连接需要关闭');
    }
  }

  public getSession(): Session | null {
    if (!this.driver) {
      if (!this.mockMode) {
        throw new Error('Neo4j 数据库未连接');
      }
      return null;
    }
    
    return this.driver.session();
  }

  // 获取所有场景节点和关系
  public async getAllScenes(): Promise<{nodes: any[], links: any[]}> {
    try {
      if (this.mockMode) {
        console.log('模拟模式: 返回模拟场景数据');
        return this.getMockSceneData();
      }

      const query = `
        MATCH (n:Scene)
        OPTIONAL MATCH (n)-[r:CONTAINS]->(m:Scene)
        RETURN n, r, m
      `;

      const records = await this.executeQuery(query);
      
      const nodes: any[] = [];
      const links: any[] = [];
      const nodeMap = new Map<string, boolean>();

      records.forEach((record: Neo4jRecord | MockRecord) => {
        const source = record.get('n')?.properties;
        const relationship = record.get('r');
        const target = record.get('m')?.properties;

        if (source && !nodeMap.has(source.id)) {
          nodeMap.set(source.id, true);
          nodes.push({
            id: source.id,
            name: source.name,
            group: source.type || 1
          });
        }

        if (target && !nodeMap.has(target.id)) {
          nodeMap.set(target.id, true);
          nodes.push({
            id: target.id,
            name: target.name,
            group: target.type || 1
          });
        }
        
        if (relationship && source && target) {
          links.push({
            source: source.id,
            target: target.id,
            value: 1
          });
        }
      });
      
      return { nodes, links };
    } catch (error) {
      console.error('获取场景数据失败:', error);
      return this.getMockSceneData();
    }
  }
  
  // 检查是否有场景数据
  public async hasSceneData(): Promise<boolean> {
    if (this.mockMode) {
      // 在模拟模式下，假设没有数据
      return false;
    }
    
    try {
      const query = "MATCH (n:Scene) RETURN count(n) as count";
      const records = await this.executeQuery(query);
      const count = records[0]?.get('count')?.toNumber() || 0;
      return count > 0;
    } catch (error) {
      console.error('检查场景数据失败:', error);
      return false;
    }
  }
  
  // 添加模拟数据方法
  private getMockSceneData(): {nodes: any[], links: any[]} {
    return {
      nodes: [
        { id: 'town1', name: '落叶镇', group: 1 },
        { id: 'inn1', name: '醉鹿旅店', group: 2 },
        { id: 'blacksmith1', name: '铁匠铺', group: 2 },
        { id: 'market1', name: '集市', group: 2 },
        { id: 'temple1', name: '光明神殿', group: 2 },
        { id: 'bar1', name: '酒吧', group: 3 },
        { id: 'kitchen1', name: '厨房', group: 3 },
        { id: 'innRoom1', name: '客房1', group: 3 },
        { id: 'forge1', name: '锻造间', group: 3 },
        { id: 'counter1', name: '吧台', group: 5 },
        { id: 'fireplace1', name: '壁炉', group: 5 }
      ],
      links: [
        { source: 'town1', target: 'inn1', value: 1 },
        { source: 'town1', target: 'blacksmith1', value: 1 },
        { source: 'town1', target: 'market1', value: 1 },
        { source: 'town1', target: 'temple1', value: 1 },
        { source: 'inn1', target: 'bar1', value: 1 },
        { source: 'inn1', target: 'kitchen1', value: 1 },
        { source: 'inn1', target: 'innRoom1', value: 1 },
        { source: 'blacksmith1', target: 'forge1', value: 1 },
        { source: 'bar1', target: 'counter1', value: 1 },
        { source: 'bar1', target: 'fireplace1', value: 1 }
      ]
    };
  }
}

export const neo4jService = Neo4jService.getInstance(); 